var form_fields = document.getElementsByTagName("input");
form_fields[1].placeholder = "Username..";
form_fields[2].placeholder = "Email..";
form_fields[3].placeholder = "Enter password...";
form_fields[4].placeholder = "Re-enter Password...";

for (var field in form_fields) {
  form_fields[field].className += " form-control";
}

function showSidebar() {
  const sidebar = document.querySelector(".sidebar");
  sidebar.style.display = "flex";
}
function hideSidebar() {
  const sidebar = document.querySelector(".sidebar");
  sidebar.style.display = "none";
}