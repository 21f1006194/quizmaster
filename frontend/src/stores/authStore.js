import { defineStore } from 'pinia';

export const useAuthStore = defineStore('auth', {
    state: () => ({
        token: localStorage.getItem('token') || null,
        isAuthenticated: !!localStorage.getItem('token'),
        role: localStorage.getItem('role') || null,
        user: localStorage.getItem('user') || null,
    }),
    actions: {
        login(token, role, user) {
            this.token = token;
            this.isAuthenticated = true;
            this.role = role;
            this.user = user;

            localStorage.setItem('token', token);
            localStorage.setItem('role', role);
            localStorage.setItem('user', user);
        },
        logout() {
            this.token = null;
            this.isAuthenticated = false;
            this.role = null;
            this.user = null;

            localStorage.removeItem('token');
            localStorage.removeItem('role');
            localStorage.removeItem('user');
        }

    }
});