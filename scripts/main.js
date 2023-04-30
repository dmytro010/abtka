document.addEventListener('DOMContentLoaded', () => {

    // Get all "navbar-burger" elements
    const $navbarBurgers = Array.prototype.slice.call(document.querySelectorAll('.navbar-burger'), 0);
  
    // Check if there are any navbar burgers
    if ($navbarBurgers.length > 0) {
  
      // Add a click event listener to each of them
      $navbarBurgers.forEach( el => {
        el.addEventListener('click', () => {
  
          // Get the target from the "data-target" attribute
          const target = el.dataset.target;
          const $target = document.getElementById(target);
  
          // Toggle the class on both the "navbar-burger" and the "navbar-menu"
          el.classList.toggle('is-active');
          $target.classList.toggle('is-active');
  
        });
      });
    }
  
    // Toggle the nested items list
    // const toggleFilesMenu = () => {
    //     const filesToggle = document.querySelector('.files-toggle');
    //     const filesMenu = document.querySelector('.files-menu');
      
    //     filesToggle.addEventListener('click', () => {
    //       filesMenu.classList.toggle('is-hidden');
    //     });
    //   };
      
    //   toggleFilesMenu();
    const toggleMenus = () => {
        const itemToggles = document.querySelectorAll('.items-toggle');
      
        itemToggles.forEach((toggle) => {
          toggle.addEventListener('click', () => {
            const menu = toggle.nextElementSibling;
            menu.classList.toggle('is-hidden');
          });
        });
      };
      
      toggleMenus();
  });
  