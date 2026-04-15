class MinStack:

    def __init__(self):
        self.stack = []
        self.min_stack = []

    def push(self, val: int) -> None:
        if not self.stack:
            self.stack = []
        if not self.min_stack:
            self.min_stack = []
        
        self.stack.append(val)
        self.min_stack.append(min(val, self.min_stack[-1] if self.min_stack else val))

    def pop(self) -> None:
        self.stack.pop()
        self.min_stack.pop()

    def top(self) -> int:
        return self.stack[-1]

    def getMin(self) -> int:
        return self.min_stack[-1]



minStack = MinStack()
minStack.push(1)
minStack.push(2)
minStack.push(0)
print(minStack.getMin()) 
minStack.pop()
print(minStack.top()) 
print(minStack.getMin()) 