import re
import tkinter as tk
from tkinter.font import Font
from tkinter import messagebox

def tokenize(string):
    # On définit les différents patterns
    patterns = [
        ('NUMBER', r'\d+(\.\d*)?'),
        ('KEYWORD', r'(sin|cos|tan|log|exp)'),
        ('OPERATOR', r'(\+|-|\*|/|\^)'),
        ('LEFT_PARENTHESIS', r'(\()'),
        ('RIGHT_PARENTHESIS', r'(\))'),
        ('WHITESPACE', r'\s+'),
        ('PI', r'pi'),
    ]

    # On crée la regex finale
    regex = '|'.join('(?P<%s>%s)' % pair for pair in patterns)

    # On crée une liste de tokens
    tokens = []

    # On parcourt la string
    for match in re.finditer(regex, string):
        # On récupère le nom du pattern
        kind = match.lastgroup

        # On récupère le contenu du pattern
        value = match.group()

        # On ajoute le token à la liste
        tokens.append((kind, value))

    if len(string) != sum(len(value) for kind, value in tokens):
            raise ValueError("La chaîne contient des caractères non valides.")

    # Remove whitespaces
    tokens = [token for token in tokens if token[0] != 'WHITESPACE']

    # On retourne la liste de tokens
    return tokens

def check_order(tokens):
    # On définit les différents patterns
    precedent_correct_order = {
        'LEFT_PARENTHESIS' : ['KEYWORD', 'OPERATOR', 'LEFT_PARENTHESIS'],
        'RIGHT_PARENTHESIS' : ['NUMBER', 'PI', 'RIGHT_PARENTHESIS'],
        'KEYWORD' : ['OPERATOR', 'LEFT_PARENTHESIS'],
        'OPERATOR' : ['NUMBER', 'PI', 'RIGHT_PARENTHESIS'],
        'NUMBER' : ['OPERATOR', 'LEFT_PARENTHESIS'],
        'PI' : ['OPERATOR', 'LEFT_PARENTHESIS'],
    }     

    stack = []
    for token in tokens:
        # On récupère le nom du pattern
        kind = token[0]

        if not stack:
            if kind == 'OPERATOR' or kind == 'RIGHT_PARENTHESIS':
                return False
            stack.append(kind)
            continue
        else:
            if stack[-1] in precedent_correct_order[kind]:
                stack.append(kind)
            else:
                return False
    if stack[-1] == 'OPERATOR' or stack[-1] == 'LEFT_PARENTHESIS' or stack.count('LEFT_PARENTHESIS') != stack.count('RIGHT_PARENTHESIS'):
        return False
    return True



# Button to calculate the result
def calculate():
    # Get the input
    input_string = input_field.get()

    # Get the output previous value
    output_string = output_field.get()

    # Check if the output field is not empty
    if output_string:
        # Delete the previous result
        output_field.config(state='normal')
        output_field.delete(0, tk.END)
        output_field.config(state='disabled')

    if not input_string:
        messagebox.showerror("Erreur", "Veuillez entrer une expression.")
        return

    # Tokenize the input
    try:
        tokens = tokenize(input_string)
    except ValueError as e:
        messagebox.showerror("Erreur", str(e))
        return

    # Calculate the result
    result = check_order(tokens)

    # Check the order of the tokens
    if not result:
        messagebox.showerror("Erreur", "L'ordre de l'expression est incorrect.")
        return

    # Display the result
    output_field.config(state='normal')
    output_field.delete(0, tk.END)
    output_field.insert(0, str(result))
    output_field.config(state='disabled')



if __name__ == "__main__":
    root = tk.Tk()
    root.configure(bg="#046380")
    root.geometry("500x500")
    root.resizable(False, False)
    root.title("Calculator")

    # Add the logo to the top middle of the frame
    logo_img = tk.PhotoImage(file="assets/calculator-logo.png")
    logo_label = tk.Label(root, image=logo_img, bg='#046380')
    logo_label.pack(side="top")

    # Input field and label
    input_label = tk.Label(root, text="Expression", bg="#046380", fg="#ffffff", font=Font(size=12, weight="bold"))
    input_label.pack(side="top")
    input_field = tk.Entry(root, width=30, borderwidth=2, foreground="#046380", background="#ffffff", highlightthickness=0, font=Font(size=12, weight="bold"))
    input_field.pack(side="top", pady=10)

    # Output field as a disabled entry
    output_label = tk.Label(root, text="Résultat", bg="#046380", fg="#ffffff", font=Font(size=12, weight="bold"))
    output_label.pack(side="top")
    output_field = tk.Entry(root, width=30, borderwidth=2, state='disabled', foreground="#046380", background="#ffffff", highlightthickness=0, font=Font(size=12, weight="bold"), disabledforeground="#046380")
    output_field.pack(side="top", pady=10)

    # Calculate button
    calculate_button = tk.Button(root, text="Calculer", padx=10, pady=10, command=calculate, bg="#046380", fg="#ffffff", activebackground="#ffffff", activeforeground="#046380", highlightthickness=0, font=Font(size=12, weight="bold"))
    calculate_button.pack(side="top", pady=10)

    root.mainloop()