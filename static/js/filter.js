const filter_options  = (  ) => {
    let select_tag = document.getElementById('filter');
    let all_commands = document.getElementsByClassName('command');
    let options = select_tag.options;
    let selected_option = options[select_tag.selectedIndex].value;
    let get_commands = document.querySelectorAll('[data-category="' + selected_option + '"]');

    if (selected_option == 'all') {
        for (let i = 0; i < all_commands.length; i++) {
            let command = all_commands[i];
            command.style.display = 'inline-block';
        }
        return;
    }

    for (let i = 0; i < all_commands.length; i++) {
        let command = all_commands[i];
        command.style.display = 'none';
    }
    if (get_commands.length > 0) {
        for (let i = 0; i < get_commands.length; i++) {
            let command = get_commands[i];
            command.style.display = 'inline-block';
        }
    }

}

const search_engine = function(e) {
    let value = e.target.value;
    let all_commands = document.getElementsByClassName('command');
    for(let i = 0; i < all_commands.length; i++) {
        if (all_commands[i].innerText.toLowerCase().includes(value.toLowerCase())) {
            all_commands[i].style.display = 'inline-block';
        }
        else {
            all_commands[i].style.display = 'none';
        }
    }
  }
const search = document.getElementById('input_search');

search.addEventListener('input', search_engine);
search.addEventListener('propertychange', search_engine); // for IE8