import { BrowserRouter, Routes, Route } from 'react-router-dom'
import HomePage from './pages/HomePage'
import LobbyPage from './pages/LobbyPage'
import ProfilePage from './pages/ProfilePage'
import RacePage from './pages/RacePage'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/lobby" element={<LobbyPage />} />
        <Route path="/profile" element={<ProfilePage />} />
        <Route path="/race" element={<RacePage />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App