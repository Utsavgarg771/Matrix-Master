// static/js/script.js
document.addEventListener('DOMContentLoaded', () => {
    const dimensionForm = document.getElementById('dimension-form');
    const matrixForm = document.getElementById('matrix-form');
    const matrixInputsDiv = document.getElementById('matrix-inputs');
    const operationInput = document.getElementById('operation-input');

    dimensionForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const rows = parseInt(document.getElementById('rows').value);
        const columns = parseInt(document.getElementById('columns').value);

        // Clear previous inputs
        matrixInputsDiv.innerHTML = '';

        // Generate input fields
        for (let i = 0; i < rows; i++) {
            const rowDiv = document.createElement('div');
            for (let j = 0; j < columns; j++) {
                const input = document.createElement('input');
                input.type = 'number';
                input.name = `element_${i}_${j}`;
                input.required = true;
                rowDiv.appendChild(input);
            }
            matrixInputsDiv.appendChild(rowDiv);
        }

        // Add hidden inputs for rows and columns
        const rowsInput = document.createElement('input');
        rowsInput.type = 'hidden';
        rowsInput.name = 'rows';
        rowsInput.value = rows;
        matrixForm.appendChild(rowsInput);

        const columnsInput = document.createElement('input');
        columnsInput.type = 'hidden';
        columnsInput.name = 'columns';
        columnsInput.value = columns;
        matrixForm.appendChild(columnsInput);

        // Show the matrix form
        matrixForm.classList.remove('hidden');
    });
});

function selectOperation(operation) {
    const operationInput = document.getElementById('operation-input');
    operationInput.value = operation;
    document.getElementById('matrix-form').submit();
}

