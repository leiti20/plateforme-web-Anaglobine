function afficherSection(sectionId) {
  const sections = ['tableauBord', 'rendezVous', 'resultats', 'perosnnel'];
  sections.forEach(id => {
    document.getElementById(id).style.display = (id === sectionId) ? "block" : "none";
  });
}
 
    function afficherFormulaire(action) {
      // Masquer tous les formulaires
      document.getElementById("ajouterCreneau").style.display = "none";
      document.getElementById("gestionCreneau").style.display = "none";
  
      // Afficher le formulaire correspondant à l'action choisie
      if (action === "ajouterCreneau") {
        document.getElementById("ajouterCreneau").style.display = "block";
      } else if (action === "gestionCreneau") {
        document.getElementById("gestionCreneau").style.display = "block";
      }
    }
  
    function confirmerSuppression() {
      if (confirm("Êtes-vous sûr(e) de vouloir supprimer ce créneau ?")) {
        // Ici tu pourras ajouter la logique de suppression dans ta base ou tableau
        alert("Créneau supprimé !");
      }
    }
  
    function afficherSection(sectionId) {
      // Masquer toutes les sections
      document.getElementById('tableauBord').style.display = 'none';
      document.getElementById('rendezVous').style.display = 'none';
      document.getElementById('resultats').style.display = 'none';
      document.getElementById('personnel').style.display = 'none';
  
      // Afficher la section demandée
      document.getElementById(sectionId).style.display = 'block';
  }
  