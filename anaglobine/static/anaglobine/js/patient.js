document.getElementById("btnInfos").addEventListener("click", () => {
  let infos = document.getElementById("infosSection");
  new bootstrap.Collapse(infos, {
    toggle: true
  });
});
  
  document.getElementById("btnHistorique").addEventListener("click", () => {
    let histo = document.getElementById("historiqueSection");
    new bootstrap.Collapse(histo, {
      toggle: true
    });
  });
   

  document.getElementById("btnSettings").addEventListener("click", () => {
    const section = document.getElementById("modifSection");
    section.style.display = section.style.display === "block" ? "none" : "block";
  });
  
