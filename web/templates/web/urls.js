var urls = urls || {};

urls.status_create = function() {
    return "{% url 'web:status-create' %}";
};


urls.workgroup_user_add = function() {
    return "{% url 'web:workgroup-user-add' %}";
};


urls.workgroup_user_remove = function() {
    return "{% url 'web:workgroup-user-remove' %}";
};


urls.skill_search = function() {
    return "{% url 'web:skill-search' %}";
};
