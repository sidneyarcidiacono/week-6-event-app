const logoutButton = document.getElementById('logout-btn')

console.log(logoutButton)

logoutButton.addEventListener('click', () => {
  window.location.href = '/logout'
})
