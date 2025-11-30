function ouvrirModaleModification(button) {
  const email = button.dataset.email;
  const nom = button.dataset.nom;
  const prenom = button.dataset.prenom || ''; // Gère les valeurs null
  const role = button.dataset.role;

  // Remplissage des champs
  document.getElementById('modifierNom').value = nom;
  document.getElementById('modifierPrenom').value = prenom;
  document.getElementById('modifierEmail').value = email;
  document.getElementById('originalEmail').value = email; // Email original
  document.getElementById('modifierRole').value = role;
}

// Fonction de suppression
function confirmerSuppression(button) {
  const email = button.closest('tr').querySelector('td:nth-child(3)').innerText;
  const role = button.closest('tr').querySelector('td:nth-child(4)').innerText;

  if (confirm("Êtes-vous sûr de vouloir supprimer ce compte ?")) {
    window.location.href = `/supprimer-compte/?email=${encodeURIComponent(email)}&role=${encodeURIComponent(role)}`;
  }
}

