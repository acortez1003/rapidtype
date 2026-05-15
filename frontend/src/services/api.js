import axios from 'axios'

const api = axios.create({
    baseURL: 'http://localhost:5000'
})

api.interceptors.request.use((config) => {
    const token = localStorage.getItem('token')
    if (token) {
        config.headers.Authorization = 'Bearer ${token}'
    }
    return config
})

export const registerUser = (username, email, password) => {
    return api.post('/api/auth/register', { username, email, password })
}

export const loginUser = (login, password) => {
    return api.post('/api/auth/login', { login, password })
}
