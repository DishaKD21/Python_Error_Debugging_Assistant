import { useMemo, useState } from 'react';

function App() {
  const [files, setFiles] = useState([]);
  const [tracebackText, setTracebackText] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const fileNames = useMemo(() => files.map((file) => file.name), [files]);

  const handleFileChange = (event) => {
    setFiles(Array.from(event.target.files || []));
  };

  const handleSubmit = async () => {
    if (!files.length) {
      setError('Please upload at least one Python file or ZIP archive.');
      return;
    }

    setLoading(true);
    setError('');

    const formData = new FormData();
    files.forEach((file) => formData.append('files', file));
    formData.append('traceback_text', tracebackText || '');

    try {
      const response = await fetch('http://127.0.0.1:8001/api/debug', {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.detail || 'The backend could not analyze the uploaded files.');
      }

      setResult(data);
    } catch (err) {
      setError(err.message || 'An unexpected error occurred.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-shell">
      <header className="topbar">
        <div>
          <span className="brand">🐍 Python Debugging Assistant</span>
        </div>
      </header>

      <main className="layout">
        <section className="panel uploader-panel">
          <h2>Upload Python files</h2>

          <label className="dropzone">
            <input type="file" multiple accept=".py,.zip" onChange={handleFileChange} />
            <span>📁 Drag & drop or choose Python files / ZIP project</span>
          </label>

          <div className="file-list">
            {fileNames.length ? (
              fileNames.map((name) => <div key={name} className="file-pill">✓ {name}</div>)
            ) : (
              <p className="muted">No files selected yet.</p>
            )}
          </div>

          <div className="field-label">Optional traceback or error context</div>
          <textarea
            rows={10}
            value={tracebackText}
            onChange={(event) => setTracebackText(event.target.value)}
            placeholder="Paste any traceback, stack trace, or error output if available"
          />

          <button className="primary-button" onClick={handleSubmit} disabled={loading}>
            {loading ? 'Analyzing...' : '🔍 Debug Code'}
          </button>

          {error && <div className="error-box">{error}</div>}
        </section>

        <section className="panel result-panel">
          <h2>Result</h2>

          {!result && !loading && (
            <div className="empty-state">
              Upload one or more Python files and click Debug Code.
            </div>
          )}

          {result && (
            <div className="result-content">
              {result.status === 'no_error' ? (
                <div className="result-block">
                  <h3>✅ No Error Detected</h3>
                  <p>{result.explanation || 'The uploaded Python code appears to be valid.'}</p>
                </div>
              ) : (
                <>
                  <div className="status-row">
                    <h3>{result.error?.type || 'ERROR DETECTED'}</h3>
                  </div>

                  <div className="summary-grid">
                    <div>
                      <label>Location</label>
                      <p>{result.error?.file || 'Not available'}:{result.error?.line ?? 'n/a'}</p>
                    </div>
                    <div>
                      <label>Message</label>
                      <p>{result.error?.message || 'Not available'}</p>
                    </div>
                  </div>

                  <div className="result-block">
                    <h4>Root Cause</h4>
                    <p>{result.root_cause || 'No root cause was provided.'}</p>
                  </div>

                  <div className="result-block">
                    <h4>Explanation</h4>
                    <p>{result.explanation || 'No additional explanation was provided.'}</p>
                  </div>

                  {result.corrected_code && (
                    <div className="result-block">
                      <h4>Corrected Code</h4>
                      <pre>{result.corrected_code}</pre>
                    </div>
                  )}

                  {result.changes && (
                    <div className="result-block">
                      <h4>What Changed</h4>
                      <p>{result.changes}</p>
                    </div>
                  )}

                  {result.tests && result.tests.length > 0 && (
                    <div className="result-block">
                      <h4>Relevant Tests</h4>
                      {result.tests.map((test, index) => (
                        <div key={`${test.name || 'test'}-${index}`} className="code-box">
                          <div className="code-header">{test.name || `Test ${index + 1}`}</div>
                          <pre>{test.code}</pre>
                        </div>
                      ))}
                    </div>
                  )}
                </>
              )}
            </div>
          )}
        </section>
      </main>
    </div>
  );
}

export default App;
