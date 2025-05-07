import { defineStore } from 'pinia';

export const useAuthStore = defineStore('auth', {
    state: () => ({
        token: localStorage.getItem('token') || null,
        isAuthenticated: !!localStorage.getItem('token'),
        role: localStorage.getItem('role') || null,
    }),
    actions: {
        login(token, role) {
            this.token = token;
            this.isAuthenticated = true;
            this.role = role;

            localStorage.setItem('token', token);
            localStorage.setItem('role', role);
        },
        logout() {
            this.token = null;
            this.isAuthenticated = false;
            this.role = null;

            localStorage.removeItem('token');
            localStorage.removeItem('role');
        }

    }
});