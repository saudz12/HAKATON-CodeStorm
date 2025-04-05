hakaton proiect
dezvoltat in python + flask pentru backend si angular pentru frontend

# Educational AI Assistant - Usage Examples

Below are examples showing how to use the Educational AI Assistant in both modes.

## Starting the Application

```bash
python interactive_app.py
```

## Basic Commands

### Switching Modes

```
> mode guide
Mode set to Educational Guidance. I will guide you through learning without providing direct answers.

> mode qa
QA mode requires a PDF to be loaded first. Please load a PDF using the load_pdf method.
Please enter the path to a PDF file: textbooks/calculus.pdf
PDF loaded successfully: textbooks/calculus.pdf. 42 chunks created.
```

### Loading a PDF

```
> load textbooks/physics.pdf
PDF loaded successfully: textbooks/physics.pdf. 37 chunks created.
PDF loaded. Would you like to switch to QA mode? (y/n): y
Mode set to Question Answering. I will provide direct answers based on the PDF content.
```

### Clearing Conversation History

```
> clear
Conversation history cleared.
```

## Guide Mode Examples

### Math Problem

```
> mode guide
Mode set to Educational Guidance. I will guide you through learning without providing direct answers.

> Solve the quadratic equation: 2x² - 5x - 3 = 0

AI Assistant:
I see you're working with a quadratic equation. Let's approach this methodically without jumping straight to the answer.

First, let's identify the coefficients in the standard form ax² + bx + c = 0:
- a = 2
- b = -5
- c = -3

For quadratic equations, we have several methods we can use:
1. Factoring
2. Completing the square
3. The quadratic formula

Let's start with factoring since the coefficients are small integers. We need to find two numbers that multiply to give a×c = 2×(-3) = -6 and add up to b = -5.

Can you think of two numbers that multiply to give -6 and add up to -5? Try to identify these factors, and then we can proceed to the next step.

If you're having trouble with factoring, let me know and we can try the quadratic formula instead.
```

### Science Problem

```
> How does photosynthesis work?

AI Assistant:
Let's explore photosynthesis together! This is a fundamental process in plants, but rather than simply giving you the complete explanation, I'll guide you through understanding it step by step.

First, can you tell me what you already know about photosynthesis? What do you think are the main inputs and outputs of this process?

Once we establish your current understanding, we can build on that knowledge by exploring:
- The key components involved in photosynthesis
- Where in the plant this process occurs
- The stages of the photosynthesis process
- How energy transformation happens during photosynthesis

Take a moment to share what you currently know, and we'll develop your understanding from there.
```

## QA Mode Examples

### Factual Question

```
> mode qa
Mode set to Question Answering. I will provide direct answers based on the PDF content.

> What is Newton's First Law?

AI Assistant:
According to the document (Chapter 3, page 78), Newton's First Law states that "an object at rest stays at rest and an object in motion stays in motion with the same speed and in the same direction unless acted upon by an unbalanced force." The textbook explains that this is also known as the law of inertia, and it demonstrates that objects resist changes to their state of motion. There's an example in the text about how a book on a table remains at rest until a force is applied to it.

Tokens used: 174 (input: 112, output: 62)
```

### Definition Request

```
> Define the derivative in calculus

AI Assistant:
According to the textbook (Chapter 2, page 34), the derivative is defined as "the instantaneous rate of change of a function with respect to its variable." The document formally expresses this as:

The derivative of a function f(x) is defined as:
f'(x) = lim(h→0) [f(x+h) - f(x)]/h

The text explains that the derivative measures the slope of the tangent line to the curve of the function at a given point. On page 35, it states that derivatives are fundamental to differential calculus and are used to analyze how functions change, find rates of change, and determine the slope at any point on a curve.

Tokens used: 198 (input: 127, output: 71)
```
