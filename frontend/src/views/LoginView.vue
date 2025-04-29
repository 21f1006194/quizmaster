<script setup>

</script>

<template>

<div class="container d-flex justify-content-center align-items-center vh-100">
    <div class="card p-4 shadow-lg" style="width: 400px;">
      <h3 class="text-center mb-4">Login</h3>
      <form>
        <div class="mb-3">
          <label for="username" class="form-label">Username</label>
          <input type="text" class="form-control" id="username" placeholder="Enter your username">
        </div>
        <div class="mb-3">
          <label for="password" class="form-label">Password</label>
          <input type="password" class="form-control" id="password" placeholder="Enter your password">
        </div>
        <div class="mb-3">
          <label for="role" class="form-label">Role</label>
          <select class="form-select" id="role" aria-label="Select your role">
            <option value="user" selected>User</option>
            <option value="admin">Admin</option>
          </select>
        </div>
        <div class="d-flex justify-content-between align-items-center">
          <div class="form-check">
            <input type="checkbox" class="form-check-input" id="remember">
            <label class="form-check-label" for="remember">Remember me</label>
          </div>
          <a href="#" class="text-decoration-none">Forgot password?</a>
        </div>
        <div class="d-grid mt-4">
          <button type="submit" class="btn btn-primary">Login</button>
        </div>
        <p class="text-center mt-3 mb-0">
          Don't have an account? <a href="#" class="text-decoration-none">Sign Up</a>
        </p>
      </form>
    </div>
  </div>

</template>