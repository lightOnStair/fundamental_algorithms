import traceback

#huffman_encode: Takes in a single String input_string, which is
# the string to be encoded.  Computes the optimal binary encoding
# of the string and encodes it, returning a String of 0s and 1s.
# This is not an actual Python binary string, just a normal String
# that happens to contain only 0s and 1s.
class Task:
    def __init__(self,char,priority):
        self.char = char
        self.priority = priority
        self.left = None
        self.right = None

def charnodes(input_string):
    task_heap = [Task(input_string[0],0)]
    for char in input_string:
        for task in task_heap:
            if task.char == char:
                task.priority += 1
                break
            if task_heap.index(task) == len(task_heap)-1:
                task_heap.append(Task(char,1))
                break
    return task_heap

def heapify(heap,i):
    small = i
    l = i*2+1
    r = i*2+2
    if l<len(heap) and heap[i].priority > heap[l].priority:
        small = l
    if r<len(heap) and heap[small].priority > heap[r].priority:
        small = r
    if small != i:
        heap[i],heap[small] = heap[small],heap[i]
        heapify(heap,small)

def build(heap):
    l = len(heap)
    for i in range(len(heap)//2-1, -1, -1):
        heapify(heap,i)
    return heap



def getmin(task_heap):
    if len(task_heap) < 1:
        return None
    max = task_heap[0]
    task_heap[0] = task_heap[len(task_heap)-1]
    task_heap.pop()
    heapify(task_heap,0)
    return max

def getParent(i):
    parent_index = (i-1) // 2
    return parent_index

def insert(task_heap,task):
    task_heap.append(task)
    increase_task_priority(task_heap,len(task_heap)-1,task.priority)

def increase_task_priority(heap,i,new_priority):
    if new_priority < heap[i].priority:
        return None
    heap[i].priority = new_priority
    while i>0 and heap[getParent(i)].priority > heap[i].priority:
        heap[i],heap[getParent(i)] = heap[getParent(i)],heap[i]
        i = getParent(i)

def build_tree(input_string):
    minQ = build(charnodes(input_string))
    for i in range(len(minQ)-1):
        low = getmin(minQ)
        low2 = getmin(minQ)
        super_ch = low.char + low2.char
        super_freq = low.priority + low2.priority
        super_node = Task(super_ch,super_freq)
        super_node.left = low
        super_node.right = low2
        insert(minQ,super_node)
    return getmin(minQ)

def encode(ch, root):
    code = ""
    node = root
    while (ch != node.char):
        if (ch in node.left.char):
            node = node.left
            code = code + "0"
        elif (ch in node.right.char):
            node = node.right
            code = code + "1"
    return code

def huffman_encode(input_string):
    root = build_tree(input_string)
    code = ""
    for ch in input_string:
        code += encode(ch,root)
    return code

a = charnodes("huh")
for i in a:
    print(i.char)
    print(i.priority)
    print("")
b = build(a)
for i in b:
    print(i.char)
    print(i.priority)
    print("")



#  DO NOT EDIT BELOW THIS LINE

tests = ['message0.txt','message1.txt','message2.txt','message3.txt',
         'message4.txt','message5.txt']
correct = ['message0encoded.txt','message1encoded.txt',
           'message2encoded.txt','message3encoded.txt',
           'message4encoded.txt','message5encoded.txt']


#Run test cases, check whether encoding correct
count = 0

try:
    for i in range(len(tests)):
        ("\n---------------------------------------\n")
        print("TEST #",i+1)
        print("Reading message from:",tests[i])
        fp = open(tests[i])
        message = fp.read()
        fp.close()
        print("Reading encoded message from:",correct[i])
        fp2 = open(correct[i])
        encoded = fp2.read()
        fp2.close()
        output = huffman_encode(message)
        if i < 5:
            print("Running: huffman_encode on '"+message+"'\n")
            print("Expected:",encoded,"\nGot     :",output)
        assert encoded == output, "Encoding incorrect!"
        print("Test Passed!\n")
        count += 1
except AssertionError as e:
    print("\nFAIL: ",e)
except Exception:
    print("\nFAIL: ",traceback.format_exc())


print(count,"out of",len(tests),"tests passed.")
