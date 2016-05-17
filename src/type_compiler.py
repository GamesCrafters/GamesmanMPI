def new_type(self, t, name, dim=*args):
    '''
    Create a new type for the compiler.
    Args is optional
    '''
    field = t
    for arg in args:
        field += '[' + args + ']'
    return field + ' ' + name + ';\n'
    
def write_types(*args):
    '''
    Takes a series of types and writes them to
    the structure to job.c
    '''
    structure = '''
enum Job_Types {
    FINISHED,
    LOOK_UP,
    RESOLVE,
    SEND_BACK,
    DISTRIBUTE,
    CHECK_FOR_UPDATES,
};

typedef struct Job
{
    int job_type;
'''
    for arg in args:
       structure += arg

    structure += '''
} Job;
    '''
    with open("job.c", "w") as job_file:
        # Make sure to clear it before we start
        job_file.truncate()
        job_file.write(structure)
