import { Route, Routes, Link } from 'react-router-dom';
import { Chat } from './chat';

export function App() {
  return (
    <div>
      <Routes>
        <Route path="/" element={<Chat />} />
        <Route path="/chat" element={<Chat />} />
        <Route
          path="/about"
          element={
            <div
              style={{ padding: '2rem', maxWidth: '800px', margin: '0 auto' }}
            >
              <h1>About ITTI Chat App</h1>
              <p>
                This is a sample chat application built with React and FastAPI
                for the ITTI technical test.
              </p>
              <p>Features:</p>
              <ul>
                <li>Real-time chat interface</li>
                <li>FastAPI backend integration</li>
                <li>Responsive design</li>
                <li>Built with Nx monorepo</li>
              </ul>
              <nav style={{ marginTop: '2rem' }}>
                <Link to="/" style={{ marginRight: '1rem', color: '#007bff' }}>
                  Go to Chat
                </Link>
              </nav>
            </div>
          }
        />
      </Routes>
    </div>
  );
}

export default App;
