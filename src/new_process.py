from mpi4py import MPI
from .game_state import GameState
from .new_job import Job
from .utils import negate, PRIMITIVE_REMOTENESS, WIN, LOSS, \
                   TIE, DRAW, to_str, reduce_singleton, PRIMITIVES
from .cache_dict import CacheDict
from queue import PriorityQueue


class Process:
    """
    Class that defines the behavior what each process should do
    """

    __slots__ = ['rank', 'root', 'initial_pos', 'resolved',
                 'world_size', 'comm', 'isend', 'recv', 'abort',
                 'work', 'received', 'remote', '_id', '_counter',
                 '_pending', 'sent']
    IS_FINISHED = False

    def dispatch(self, job):
        """
        Given a particular kind of job, decide what to do with
        it, this can range from lookup, to distributing, to
        checking for recieving.
        """
        _dispatch_table = (
            self.finished,
            self.lookup,
            self.resolve,
            self.send_back,
            self.distribute,
            self.check_for_updates
        )
        return _dispatch_table[job.job_type](job)

    def run(self):
        """
        Main loop for each process
        """
        while not Process.IS_FINISHED:
            if (
                self.rank == self.root and
                self.initial_pos.pos in self.resolved
               ):
                Process.IS_FINISHED = True
                print(
                    to_str(self.resolved[self.initial_pos.pos]) +
                    " in " +
                    str(self.remote[self.initial_pos.pos]) +
                    " moves"
                )
                self.abort()
            if self.work.empty():
                self.work.put(Job(Job.CHECK_FOR_UPDATES))
            job = self.work.get()
            result = self.dispatch(job)
            if result is None:  # Check for updates returns nothing.
                continue
            self.work.put(result)

    def __init__(self, rank, world_size, comm,
                 isend, recv, abort, stats_dir=''):
        self.rank = rank
        self.world_size = world_size
        self.comm = comm

        self.isend = isend
        self.recv = recv
        self.abort = abort

        self.initial_pos = GameState(GameState.INITIAL_POS)
        self.root = self.initial_pos.get_hash(self.world_size)

        self.work = PriorityQueue()
        self.resolved = CacheDict("resolved", stats_dir, self.rank)
        self.remote = CacheDict("remote", stats_dir, self.rank)
        # Keep a dictionary of "distributed tasks"
        # Should contain an id associated with the length of task.
        # For example, you distributed rank 0 has 4, you wish to
        # distribute 3, 2. Give it an id, like 1 and associate it
        # with length 2. Then once all the results have been received
        # you can compare the length, and then reduce the results.
        # solving this particular distributed task.

        # Job id tracker.
        self._id = 0
        # A job_id -> Number of results remaining.
        self._counter = CacheDict("counter", stats_dir, self.rank, t="work")
        # job_id -> [ Job, GameStates, ... ]
        self._pending = CacheDict("pending", stats_dir, self.rank, t="work")

        # Keep track of sent requests
        self.sent = []

    def finished(self, job):
        """
        Occurs when the root node has detected that the game has been solved
        """
        self.IS_FINISHED = True

    def lookup(self, job):
        """
        Takes a GameState object and determines if it is in the
        resolved list. Returns the result if this is the case, None
        otherwise.
        """
        gs_tup = (job.gs_pos, job.gs_prim, job.gs_remoteness)
        try:
            # job.game_state.state = self.resolved[job.game_state.pos]
            # job.game_state.remoteness = self.remote[job.game_state.pos]
            # return Job(Job.SEND_BACK, job.game_state, job.parent, job.job_id)

            prim = self.resolved[job.gs_pos]
            remoteness = self.remote[job.gs_pos]
            return Job(Job.SEND_BACK, job.parent, job.job_id,
                       (job.gs_pos, prim, remoteness))
        except KeyError:  # Not in dictionary
            # Try to see if it is_primitive:
            if job.gs_prim in PRIMITIVES:
            # if job.game_state.is_primitive():
                self.remote[job.gs_pos] = PRIMITIVE_REMOTENESS
                job.gs_remoteness = PRIMITIVE_REMOTENESS
                self.resolved[job.gs_pos] = job.gs_prim
                return Job(
                    Job.SEND_BACK,
                    job.parent,
                    job.job_id,
                    gs_tup
                )
            # Not a primitive.
            return Job(Job.DISTRIBUTE, job.parent, job.job_id,
                       gs_tup)

    def _add_pending_state(self, job, children):
        self._pending[self._id] = [job]
        self._counter[self._id] = len(list(children))

    def _update_id(self):
        """
        Changes the id so there is no collision.
        """
        self._id += 1

    def distribute(self, job):
        """
        Given a gamestate distributes the results to the appropriate
        children.
        """
        children = list(GameState.expand(job.gs_pos))
        # Add new pending state information.
        self._add_pending_state(job, children)
        # Keep a list of the requests made by isend. Something may
        # fail, so we will need to worry about error checking at
        # some point.
        for child in children:
            new_job = Job(Job.LOOK_UP, self.rank, self._id,
                          (child.pos, child.state, child.remoteness))
            req = self.isend(new_job, dest=child.get_hash(self.world_size))
            self.sent.append(req)

        self._update_id()

    def check_for_updates(self, job):
        """
        Checks if there is new data from other Processes that needs to
        be received and prepares to recieve it if there is any new data.
        Returns True if there is new data to be recieved.
        Returns None if there is nothing to be recieved.
        """
        for req in self.sent[:]:
            if req.test()[0]:
                self.sent.remove(req)

        # If there are sources recieve them.
        while self.comm.Iprobe():
            self.work.put(self.recv())

    def send_back(self, job):
        """
        Send the job back to the node who asked for the computation
        to be done.
        """
        gs_tup = (job.gs_pos, job.gs_prim, job.gs_remoteness)
        resolve_job = Job(Job.RESOLVE, job.parent, job.job_id, gs_tup)
        req = self.isend(resolve_job, dest=resolve_job.parent)
        self.sent.append(req)

    def _res_red(self, child_states):
        """
        Private method that helps reduce in resolve.
        """

        if TIE in child_states:
            return TIE
        if LOSS in child_states:
            return WIN
        return LOSS

    def _remote_red(self, state, children):
        """
        Private method that helps reduce remoteness.
        Takes in the state of the current gamestate and the remoteness of the
        children.
        """
        if state == WIN:
            losers = filter(lambda c: c[1] == LOSS, children)
            remotes = [loser[2] for loser in losers]
            return min(remotes)
        elif state == LOSS:
            remotes = [child[2] for child in children]
            return max(remotes)
        elif state == TIE:
            ties = filter(lambda c: c[0] == TIE, children)
            remotes = [tie[2] for tie in ties]
            return max(remotes)

    def _cleanup(self, job):
        del self._pending[job.job_id][:]
        del self._pending[job.job_id]
        del self._counter[job.job_id]

    def resolve(self, job):
        """
        Given a list of WIN, LOSS, TIE, (DRAW, well maybe for later)
        determine whether this position in the game tree is a WIN,
        LOSS, TIE, or DRAW.
        """
        self._counter[job.job_id] -= 1
        # [Job, GameState, ... ]

        if len(self._pending[job.job_id]) == 1:
            self._pending[job.job_id].append(job.gs_tuple())
        else:
            curr_gs_tup = self._pending[job.job_id][1]
            self._pending[job.job_id][1] = GameState.compare_gamestates(curr_gs_tup, job.gs_tuple())

        # Resolve _pending
        if self._counter[job.job_id] == 0:
            # [Job, GameState, ...] -> Job
            to_resolve = self._pending[job.job_id][0]
            best_gs = self._pending[job.job_id][1]
            if to_resolve.gs_prim in PRIMITIVES:
            # if to_resolve.game_state.is_primitive():
                self.resolved[to_resolve.gs_pos] = \
                    to_resolve.gs_prim
                self.remote[to_resolve.gs_pos] = 0
            else:
                self.resolved[to_resolve.gs_pos] = self._res_red([best_gs[1]])
                self.remote[to_resolve.gs_pos] = best_gs[2] + 1
                job.gs_prim = self.resolved[to_resolve.gs_pos]
                job.gs_remoteness = \
                    self.remote[to_resolve.gs_pos]

            to = Job(
                Job.SEND_BACK,
                to_resolve.parent,
                to_resolve.job_id,
                (job.gs_pos,
                job.gs_prim,
                job.gs_remoteness)
            )
            self.work.put(to)
            # Dealloc unneeded _pending and counter data.
            self._cleanup(job)