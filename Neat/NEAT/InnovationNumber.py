class InnovationNumber:
    innov_number = 0
    innovations = {}

    '''
    Set key=(in, out) nodes and value = number. Static because this is tracked throughout the environment.
    '''
    @staticmethod
    def get_innovation_number(in_, out):
        key = (in_.node_id, out.node_id)
        if key not in InnovationNumber.innovations.keys():
            InnovationNumber.innov_number += 1
            InnovationNumber.innovations[key] = InnovationNumber.innov_number
        return InnovationNumber.innovations[key]
