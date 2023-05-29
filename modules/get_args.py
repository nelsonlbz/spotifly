# * ====== ARGS INITIALIZATION ====== *
def quick_initialize_args(**args):
    class Args:
        def __init__(self, **args):
            for arg in args:
                setattr(self, arg, args[arg])
            return 
    return Args(**args)
