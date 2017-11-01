class Job:
    """
    A job has a game state, parent, type, and also has a priority for placing
    jobs in a queue for the processes to work on.
    """

    __slots__ = ['job_type', 'priority', 'game_state', 'parent', 'job_id']

    # A list of possible job types.
    FINISHED          = 0
    LOOK_UP           = 1
    RESOLVE           = 2
    SEND_BACK         = 3
    DISTRIBUTE        = 4
    CHECK_FOR_UPDATES = 5

    # Special number associated with the initial job id.
    INITIAL_JOB_ID = 0

    def _assign_priority(self):
        self.priority = self.job_type

    def __init__(self, job_type, game_state=None, parent=None, job_id=None):
        self.job_type   = job_type
        self.game_state = game_state
        self.parent     = parent
        self.job_id     = job_id
        self._assign_priority()

    def __lt__(self, other):
        """
        Compares two Job objects based off the priority
        they have.
        """
        return self.priority < other.priority
