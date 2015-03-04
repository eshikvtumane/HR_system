div_name = 'edu_';
btn = document.getElementById('add_form')
btn_remove = document.getElementById('remove_form');

//Добавление формы
  function addEducationForm(div_forms){

    btn_value = btn.value;

    div = document.getElementById(div_name+btn_value);
    clone = div.cloneNode(true);

    id = parseInt(btn_value) + 1;
    clone.id = 'edu_' + id;
    btn.value = id.toString();
    btn_remove.value = id.toString();


    document.getElementById(div_forms).appendChild(clone);
  }

  function removeEducationForm(){

    remove_val = btn_remove.value;

    if(remove_val != '1'){
        document.getElementById(div_name + remove_val).remove()
        btn.value = (remove_val - 1).toString();
        btn_remove.value = (remove_val - 1).toString();
    }
  }

  <!-- Определение функции удаления элементов -->
    Element.prototype.remove = function() {
        this.parentElement.removeChild(this);
    }
    NodeList.prototype.remove = HTMLCollection.prototype.remove = function() {
        for(var i = 0, len = this.length; i < len; i++) {
            if(this[i] && this[i].parentElement) {
                this[i].parentElement.removeChild(this[i]);
            }
        }
    }