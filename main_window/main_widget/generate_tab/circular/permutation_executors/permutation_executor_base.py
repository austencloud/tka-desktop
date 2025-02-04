class PermutationExecutor:
    """Base class to hold the function signature for creating permutations."""

    def create_permutations(self, sequence: list[dict]):
        raise NotImplementedError("This method should be overridden by subclasses.")
