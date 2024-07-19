# Backtrack

Status: algorithm, yet
Theme: recursive
Created time: November 17, 2023 4:21 PM
Last edited time: November 17, 2023 4:22 PM

- [ ]  한국어 번역하면서 정리
1. **Choose**: Start by choosing an option among many available at the current step.
2. **Constrain**: Apply constraints to check if the current choice leads to a solution or not. If the choice does not satisfy the constraints, this is known as a "dead end."
3. **Goal Check**: Check if the current choice leads to a solution. If the goal is achieved, return the solution.
4. **Recursion**: If the current choice does not lead to a solution but also is not a dead end, recursively apply the backtracking algorithm with this choice included as part of the solution.
5. **Backtrack**: If the current choice leads to a dead end, discard it and go back (backtrack) to the previous step to try a different option.
6. **Iterate**: Continue this process of choosing, constraining, goal checking, recursion, and backtracking until all options have been tried and the solution is found or it's determined that no solution exists.