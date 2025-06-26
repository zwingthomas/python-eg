from collections import deque

dq = deque((3, 4, 5))
print(dq)
dq.append(6)
print(dq)
dq.appendleft(2)
print(dq)
dq.popleft()
print(dq)
dq.pop()
print(dq)


def is_palindrome(word):
    dq = deque(word)
    while len(dq) > 1:
        if dq.popleft() != dq.pop():
            return False
    return True


print(is_palindrome("racecar"))
print(is_palindrome("thomas"))
