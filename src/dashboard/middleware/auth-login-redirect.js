export default function ({ $auth, redirect }) {
    if (!$auth.loggedIn) {
      return redirect('/login'); // Redirect to the login page if the user is not logged in
    }
  }