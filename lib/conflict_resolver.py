from gpt_api import GPT


class CodeConflictResolver:
    def __init__(self):
        self.gpt = GPT()

    def resolve(self, original_line, change_1, change_2):
        # Create a prompt for GPT
        prompt = "You are developing an automated conflict resolution system for merging two proposed changes " \
                 "to a Python function. The system will prioritize preserving logic and optimizing code readability" \
                 " according to PEP-8 guidelines." \
                 f" The original line of code is '{original_line}'. One change is '{change_1}'," \
                 f" and the second change is '{change_2}'." \
                 " Your goal is to create an automated process that resolves conflicts while adhering to PEP-8" \
                 " and producing readable code."

        # Send the prompt to GPT and get the resolution
        resolution = self.gpt.chat(prompt)

        return resolution


if __name__ == '__main__':
    resolver = CodeConflictResolver()
    print(resolver.resolve("if var:", "if n_values:", "if n_values != 0:"))