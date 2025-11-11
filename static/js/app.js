const uploadBox = document.getElementById('uploadBox');
const fileInput = document.getElementById('fileInput');
const statusMessage = document.getElementById('statusMessage');
const resultSection = document.getElementById('resultSection');
const characterName = document.getElementById('characterName');
const viewBtn = document.getElementById('viewBtn');
const downloadBtn = document.getElementById('downloadBtn');

let currentOutputFile = '';

uploadBox.addEventListener('click', () => {
    fileInput.click();
});

uploadBox.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadBox.classList.add('dragging');
});

uploadBox.addEventListener('dragleave', () => {
    uploadBox.classList.remove('dragging');
});

uploadBox.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadBox.classList.remove('dragging');
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        handleFile(files[0]);
    }
});

fileInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
        handleFile(e.target.files[0]);
    }
});

function showStatus(message, type) {
    statusMessage.textContent = message;
    statusMessage.className = `status-message ${type}`;
    statusMessage.classList.remove('hidden');
}

function hideStatus() {
    statusMessage.classList.add('hidden');
}

function showResult(fileName, charName) {
    currentOutputFile = fileName;
    characterName.textContent = `Character: ${charName}`;
    resultSection.classList.remove('hidden');
}

function hideResult() {
    resultSection.classList.add('hidden');
}

async function handleFile(file) {
    if (!file.name.endsWith('.json')) {
        showStatus('Please select a valid JSON file', 'error');
        return;
    }

    hideResult();
    showStatus('Processing character data...', 'loading');

    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (response.ok && data.success) {
            showStatus('Character sheet generated successfully!', 'success');
            showResult(data.output_file, data.character_name);
        } else {
            showStatus(`Error: ${data.error || 'Failed to generate character sheet'}`, 'error');
        }
    } catch (error) {
        showStatus(`Error: ${error.message}`, 'error');
    }
}

viewBtn.addEventListener('click', () => {
    if (currentOutputFile) {
        window.open(`/view/${currentOutputFile}`, '_blank');
    }
});

downloadBtn.addEventListener('click', () => {
    if (currentOutputFile) {
        window.location.href = `/download/${currentOutputFile}`;
    }
});
