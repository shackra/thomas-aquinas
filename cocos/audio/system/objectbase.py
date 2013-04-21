##########################################################################################
#================================== ObjectBase class ====================================#
##########################################################################################

class ObjectBase(object):
    """
    Abstract base class for the SFML class wrappers.
    """

    def __init__(self, this_pointer):
        """
        Initialise a new ObjectBase object.

        :param this_pointer: The pointer to the CSFML object.
        """
        super(ObjectBase, self).__init__()

        self.this = this_pointer

##########################################################################################
