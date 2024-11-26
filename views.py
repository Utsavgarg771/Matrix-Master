# calculator/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
import numpy as np
from django.contrib.auth import login, logout
from scipy.linalg import lu, svd, eig
from .models import MatrixHistory
from django.contrib.auth.decorators import login_required

def echelon_form(matrix):
    m = np.array(matrix, dtype=float)
    rows, cols = m.shape
    for i in range(min(rows, cols)):
        # Find the pivot
        max_row = np.argmax(abs(m[i:, i])) + i
        if m[max_row, i] == 0:
            continue
        # Swap rows
        m[[i, max_row]] = m[[max_row, i]]
        # Eliminate below
        for j in range(i + 1, rows):
            factor = m[j, i] / m[i, i]
            m[j, i:] -= factor * m[i, i:]
    return np.around(m, decimals=2)

def reduced_row_echelon_form(matrix):
    m = np.array(matrix, dtype=float)
    rows, cols = m.shape
    lead = 0
    for r in range(rows):
        if lead >= cols:
            return np.around(m, decimals=2)
        i = r
        while m[i, lead] == 0:
            i += 1
            if i == rows:
                i = r
                lead += 1
                if cols == lead:
                    return np.around(m, decimals=2)
        m[[r, i]] = m[[i, r]]
        lv = m[r, lead]
        m[r] = m[r] / lv
        for i in range(rows):
            if i != r:
                lv = m[i, lead]
                m[i] -= lv * m[r]
        lead += 1
    return np.around(m, decimals=2)


def index(request):
    result = None
    if request.method == 'POST' and 'operation' in request.POST:
        operation = request.POST.get('operation')
        rows = int(request.POST.get('rows'))
        columns = int(request.POST.get('columns'))

        # Reconstruct the matrix from POST data
        matrix = []
        for i in range(rows):
            row = []
            for j in range(columns):
                element = float(request.POST.get(f'element_{i}_{j}'))
                row.append(element)
            matrix.append(row)
        matrix = np.array(matrix)

        try:
            if operation == 'determinant':
                if rows == columns:
                    result_value = np.linalg.det(matrix)
                    result = f"The determinant is {result_value}."
                else:
                    result = "Determinant is only defined for square matrices."
            elif operation == 'rank':
                result_value = np.linalg.matrix_rank(matrix)
                result = f"The rank is {result_value}."
            elif operation == 'echelon':
                result_matrix = echelon_form(matrix)
                result = f"The Echelon Form is:\n{result_matrix}"
            elif operation == 'rref':
                result_matrix = reduced_row_echelon_form(matrix)
                result = f"The Reduced Row Echelon Form is:\n{result_matrix}"
            elif operation == 'trace':
                if rows == columns:
                    result_value = np.trace(matrix)
                    result = f"The trace is {result_value}."
                else:
                    result = "Trace is only defined for square matrices."
            elif operation == 'inverse':
                if rows == columns:
                    try:
                        result_matrix = np.linalg.inv(matrix)
                        result = f"The inverse is:\n{result_matrix}"
                    except np.linalg.LinAlgError:
                        result = "The matrix is singular and cannot be inverted."
                else:
                    result = "Inverse is only defined for square matrices."
            elif operation == 'transpose':
                result_matrix = matrix.T
                result = f"The transpose is:\n{result_matrix}"
            elif operation == 'eigen':
                if rows == columns:
                    eigenvalues, eigenvectors = eig(matrix)
                    result = f"Eigenvalues:\n{eigenvalues}\n\nEigenvectors:\n{eigenvectors}"
                else:
                    result = "Eigenvalues and eigenvectors are only defined for square matrices."
            elif operation == 'lu':
                if rows == columns:
                    P, L, U = lu(matrix)
                    result = f"P (Permutation Matrix):\n{P}\n\nL (Lower Triangular Matrix):\n{L}\n\nU (Upper Triangular Matrix):\n{U}"
                else:
                    result = "LU Factorization is only defined for square matrices."
            elif operation == 'svd':
                U, S, VT = svd(matrix)
                result = f"U Matrix:\n{U}\n\nSingular Values:\n{S}\n\nVT Matrix:\n{VT}"
            elif operation == 'diagonalization':
                if rows == columns:
                    eigenvalues, eigenvectors = eig(matrix)
                    diagonal = np.diag(eigenvalues)
                    result = f"Diagonal Matrix:\n{diagonal}\n\nEigenvector Matrix:\n{eigenvectors}"
                else:
                    result = "Diagonalization is only defined for square matrices."
            else:
                result = "Invalid operation selected."
                
            history_entry = MatrixHistory(user=request.user, matrix_input=str(matrix), matrix_output=str(result))
            history_entry.save()
            
        except Exception as e:
            result = f"An error occurred: {e}"

    return render(request, 'index.html', {'result': result})
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            # Redirect to login page after successful registration
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


# Login view
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

# Logout view
def logout_view(request):
    logout(request)
    return redirect('index')

# User history view
@login_required
def history(request):
    user_history = MatrixHistory.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'history.html', {'history': user_history})

