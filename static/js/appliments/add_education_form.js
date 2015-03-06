

//Добавление формы
  function addForm(obj, div_forms, div_name, btn_remove){
    clone_from = div_name + obj.value;
    clone_to = div_forms;
    btn_remove_obj = document.getElementById(btn_remove);

    divClone(obj, clone_from, clone_to, obj.value, div_name, btn_remove_obj);
  }


  function removeForm(obj, btn_add, div_name){
    btn = document.getElementById(btn_add);
    remove_val = obj.value;

    if(remove_val != '1'){
        document.getElementById(div_name + remove_val).remove()
        btn.value = (remove_val - 1).toString();
        obj.value = (remove_val - 1).toString();
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


    function addVacancyForm(div_forms){

    }

    function divClone(btn, clone_from, clone_to, btn_value, div_name, btn_remove){
        div = document.getElementById(clone_from);
        clone = div.cloneNode(true);

        id = parseInt(btn_value) + 1;
        clone.id = div_name + id;
        btn.value = id.toString();
        btn_remove.value = id.toString();
        document.getElementById(clone_to).appendChild(clone);

        return;
    }