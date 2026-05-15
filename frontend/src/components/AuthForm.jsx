import { useState } from 'react'
import { useAuth } from '../context/AuthContext'
import { loginUser, registerUser } from '../services/api'
import { useNavigate } from 'react-router-dom'

function AuthForm() {
    const { setUser } = useAuth()
    const navigate = useNavigate()
    const [login, setLogin] = useState('')
    const [username, setUsername] = useState('')
    const [email, setEmail] = useState('')
    const [password, setPassword] = useState('')
    const [confirmPassword, setConfirmPassword] = useState('')
    const [isLogin, setIsLogin] = useState(true)
    const [error, setError] = useState('')

    const handleSubmit = async (e) => {
        e.preventDefault()
        try {
            if (!isLogin) {
                if (password != confirmPassword) {
                    setError('Password do not match')
                    return
                }
                const response = await registerUser(username, email, password)
                setUser({
                    username: response.data.username,
                    token: response.data.access_token
                })
                localStorage.setItem('token', response.data.access_token)
            } else {
            const response = await loginUser(login, password)
                setUser({
                    username: response.data.username,
                    token: response.data.access_token
                })
                localStorage.setItem('token', response.data.access_token)
            }
            navigate('/lobby')
        } catch (err) {
            setError(err.response?.data?.error || 'Something went wrong')
        }
    }

    return (
        <form onSubmit={handleSubmit}>
            <h2>{isLogin ? 'Login' : 'Register'}</h2>
            {isLogin && (
                <input
                    type="text"
                    placeholder="Username or Email"
                    value={login}
                    onChange={(e) => setLogin(e.target.value)}
                />
            )}
            {!isLogin && (
                <>
                    <input
                        type="text"
                        placeholder="Username"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                    />
                    <input
                        type="text"
                        placeholder="Email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                    />
                </>
            )}
            <input
                type="password"
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
            />
            {!isLogin && (
                <input
                    type="password"
                    placeholder="Confirm Password"
                    value={confirmPassword}
                    onChange={(e) => setConfirmPassword(e.target.value)}
                />
            )}
            {error && <p>{error}</p>}
            <button type="submit">Submit</button>
            <button type="button" onClick={() => setIsLogin(!isLogin)}>
                {isLogin ? 'Need an account? Register' : 'Already have an account? Login'}
            </button>
        </form>
    )
}

export default AuthForm