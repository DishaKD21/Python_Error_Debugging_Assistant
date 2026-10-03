import { useState } from "react";
import "./App.css";

function App() {
  const [files, setFiles] = useState([]);
  const [traceback, setTraceback] = useState("");
  const [dragging, setDragging] = useState(false);

  // Add Python files
  const addFiles = (newFiles) => {
    const pythonFiles = Array.from(newFiles).filter((file) =>
      file.name.toLowerCase().endsWith(".py")
    );

    if (pythonFiles.length === 0) {
      alert("Please select Python (.py) files only.");
      return;
    }

    setFiles((previousFiles) => {
      const existingNames = new Set(
        previousFiles.map((file) => file.name)
      );

      const newUniqueFiles = pythonFiles.filter(
        (file) => !existingNames.has(file.name)
      );

      return [...previousFiles, ...newUniqueFiles];
    });
  };

  // File input
  const handleFileChange = (event) => {
    addFiles(event.target.files);

    // Allows selecting the same file again
    event.target.value = "";
  };

  // Remove file
  const removeFile = (fileName) => {
    setFiles((previousFiles) =>
      previousFiles.filter((file) => file.name !== fileName)
    );
  };

  // Drag and drop
  const handleDragOver = (event) => {
    event.preventDefault();
    setDragging(true);
  };

  const handleDragLeave = () => {
    setDragging(false);
  };

  const handleDrop = (event) => {
    event.preventDefault();

    setDragging(false);

    addFiles(event.dataTransfer.files);
  };

  // Debug button
  const handleDebug = () => {
    if (files.length === 0) {
      alert("Please add at least one Python file.");
      return;
    }

    if (!traceback.trim()) {
      alert("Please enter the Python traceback.");
      return;
    }

    console.log("Selected files:", files);
    console.log("Traceback:", traceback);

    alert(
      "Frontend is ready.\n\nNext step: connect this button to your FastAPI /debug API."
    );
  };

  return (
    <div className="app">

      {/* ================= HEADER ================= */}

      <header className="header">

        <div className="brand">

          <div className="logo">
            🐍
          </div>

          <div>
            <h1>PyDebug AI</h1>

            <p>
              Python Error Debugging Assistant
            </p>
          </div>

        </div>

        <div className="status">

          <span className="status-dot"></span>

          AI Debugger

        </div>

      </header>


      {/* ================= MAIN ================= */}

      <main className="container">

        <div className="page-title">

          <h2>
            Debug Your Python Project
          </h2>

          <p>
            Upload multiple Python files and provide the traceback
            to analyze and fix the error.
          </p>

        </div>


        {/* ================= FILE UPLOAD ================= */}

        <section className="card">

          <div className="section-header">

            <div>

              <h3>
                📁 Python Project Files
              </h3>

              <p>
                Add one or multiple Python files
              </p>

            </div>


            {files.length > 0 && (

              <span className="file-count">

                {files.length}

                {" "}

                {files.length === 1
                  ? "file"
                  : "files"}

              </span>

            )}

          </div>


          {/* DROP AREA */}

          <label
            className={`drop-zone ${
              dragging ? "dragging" : ""
            }`}
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            onDrop={handleDrop}
          >

            <input
              type="file"
              multiple
              accept=".py"
              onChange={handleFileChange}
            />


            <div className="upload-icon">
              📂
            </div>


            <h3>
              Drop Python files here
            </h3>


            <p>
              or
            </p>


            <span className="choose-button">
              + Add Python Files
            </span>


            <small>
              You can select multiple .py files at once
            </small>

          </label>


          {/* ================= FILE LIST ================= */}

          {files.length > 0 && (

            <div className="file-list">

              <div className="file-list-title">
                Selected Files
              </div>


              {files.map((file) => (

                <div
                  className="file-item"
                  key={file.name}
                >

                  <div className="file-info">

                    <div className="python-icon">
                      PY
                    </div>


                    <div>

                      <strong>
                        {file.name}
                      </strong>


                      <span>
                        {(file.size / 1024).toFixed(1)}
                        {" KB"}
                      </span>

                    </div>

                  </div>


                  <button
                    className="remove-button"
                    onClick={() =>
                      removeFile(file.name)
                    }
                    title="Remove file"
                  >
                    ×
                  </button>

                </div>

              ))}

            </div>

          )}


          {/* ================= ADD MORE ================= */}

          {files.length > 0 && (

            <label className="add-more">

              <input
                type="file"
                multiple
                accept=".py"
                onChange={handleFileChange}
              />

              + Add More Files

            </label>

          )}

        </section>


        {/* ================= TRACEBACK ================= */}

        <section className="card">

          <div className="section-header">

            <div>

              <h3>
                ⚠️ Python Traceback
              </h3>

              <p>
                Paste the error traceback generated by Python
              </p>

            </div>

          </div>


          <textarea
            value={traceback}
            onChange={(event) =>
              setTraceback(event.target.value)
            }
            placeholder={`Example:

Traceback (most recent call last):
  File "main.py", line 8, in <module>
    result = divide(10, 0)

  File "calculator.py", line 3, in divide
    return a / b

ZeroDivisionError: division by zero`}
          />

        </section>


        {/* ================= DEBUG BUTTON ================= */}

        <button
          className="debug-button"
          onClick={handleDebug}
        >

          <span>
            🔍
          </span>

          Debug Python Code

        </button>


        {/* ================= FOOTER INFO ================= */}

        <div className="info">

          <span>
            🔒
          </span>

          {" "}
          Your files will be analyzed securely by
          the debugging system.

        </div>

      </main>

    </div>
  );
}

export default App;
