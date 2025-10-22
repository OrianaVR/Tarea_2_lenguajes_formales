# Context-Free Grammar - ASSIGNMENT 2

**Course:** Formal Languages and Compilers

**Class number:** 5730

**Students:**

- Ana Sofia Angarita Barrios
- Nawal Oriana Valoyes Rentería

---

## System and Tools
- **Operating System:** Windows 10
- **Programming Language:** Python 3
- **Used:** Visual Studio Code

---

## Descripcion
This project implements the algorithm for eliminating left recursion from a Context-Free Grammar (CFG), as described in Compilers: Principles, Techniques, and Tools by Aho et al. (Section 4.3.3).
For each case, print an equivalent grammar without left recursion. To print the productions, follow the same format as
in the input.

---

## Instructions for running the implementation.
**1.** Ensure a working installation of Python 3.

**2.** Save the Code: Save the provided Python code in a file named main.py.
**Run from Terminal:** Execute the script using the Python interpreter:

**3.** The program expects input in the following strict format:
- **Line 1:** A number $n > 0$ indicating the total number of cases.
- **For Each Case:** A line with a natural number $k > 0$ representing the number of nonterminals ($k=|N|$). Each containing a production in the format: nonterminal **->** derivation alternatives separated by blank spaces.

**4** : The program will print the equivalent grammar without left recursion for each case, following the same format as the input. A single line break is printed between cases.

---

## Algorithm Explanation
**1.** The algorithm establishes a fixed order for all nonterminals, $N = \{A_1, A_2, \dots, A_k\}$, and processes them in this sequence. When nonterminal $A_i$ is processed, the algorithm ensures that all left recursion involving $A_i$ and any preceding nonterminal $A_j$ ($j < i$) is completely removed.

**2.** For a nonterminal $A_i$, the code iterates through all $A_j$ where $j < i$. If a production is of the form $A_i \rightarrow A_j \gamma$, this production is replaced. The substitution involves taking all current productions of $A_j$ and substituting them back into $A_i$, resulting in new productions of the form. This step guarantees that $A_i$ will not start with any nonterminal $A_j$ that precedes it in the established order.

**3.** Once the substitution is complete, $A_i$ may only have direct left recursion, meaning productions of the form $A_i \rightarrow A_i \alpha \mid \beta$. The strings $\beta$ are the non-recursive alternatives (those not starting with $A_i$), and the strings $\alpha$ are the trailing sequences of the recursive productions. To eliminate this direct recursion, a new nonterminal ($A'$, which is sequentially named $Z, Y, X, \dots$ in the code to comply with the single capital letter requirement) is introduced.

---

## Reference

AI: Gemini AI

Books: Kozen(1997)
