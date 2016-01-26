$(function($) {
var app = {};
app.EVENT_DATA_ID = 'events_json'
//////////////////////////// DATA
app.data = {};
app.data.events = JSON.parse($('#events_json').text());
app.data.projects = JSON.parse($('#projects_json').text());

/////////////////////////// TEMPLATES
app.templates = {};

_.template.formatdate = function(date) {
    var date_obj = new Date(date);
    var hh = date_obj.getHours();
    var mm = date_obj.getMinutes();
    if(mm < 10) {mm = "0"+mm;};
    return hh + ":" + mm;
};

app.templates.event_template = _.template(`
<li id="event-<%= pk %>" class="draggable-event list-group-item" draggable="true">
    <%= fields.summary %><br>
    <%= _.template.formatdate(fields.start) %> - <%= _.template.formatdate(fields.end) %>
</li>
`);

app.templates.project_template = _.template(`
<div class="panel panel-default project" id="project-<%= pk %>">
    <div class="panel-heading"><%= fields.client_name %> - <%= fields.project_name %></div>
    <div class="panel-body" ondragover="app.allowDrop(event)">
        <ul id="events-<%= pk %>" class="list-group event-list">
        </ul>
    </div>
</div>
`)

app.templates.new_project = _.template(`
<div class="modal-dialog">
  <div class="modal-content">
    <div class="modal-header">
      <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
      <h4 class="modal-title">Create new project</h4>
    </div>
    <div class="modal-body">
        <div class="form-group">
            <label for="new-project-client">Client name</label>
            <input type="text" class="form-control" id="new-project-client" placeholder="Apple Inc.">
        </div>
        <div class="form-group">
            <label for="new-project-name">Project name</label>
            <input type="text" class="form-control" id="new-project-name" placeholder="iPhone Launch">
        </div>
        <div class="form-group">
            <label for="new-pattern">Pattern</label>
            <input type="text" class="form-control" id="new-pattern" placeholder="iPhone [L|l]aunch">
        </div>
    </div>
    <div class="modal-footer">
      <button class="btn btn-primary" id="create">Create</button>
    </div>
  </div><!-- /.modal-content -->
</div><!-- /.modal-dialog -->
`)

////////////////////////////////////// MODELS
var Event = Backbone.Model.extend({
    url: '/event',
});

var Events = Backbone.Collection.extend({
    model: Event,
    byProject: function(project_id) {
        filtered = this.filter(function(ev) {
            return ev.get('fields').project == project_id;
        });
        return new Events(filtered);
    }
});

var Project = Backbone.Model.extend({
    url: '/project',
});

var Projects = Backbone.Collection.extend({
    model: Project,
});

/////////////////////////////////////// VIEWS

var EventView = Backbone.View.extend({
    template: app.templates.event_template,
    events: {'dragstart': 'drag'},
    render: function() {
        this.$el.html(this.template(this.model.attributes));
        return this;
    },
    drag: function(ev) {
        ev.originalEvent.dataTransfer.setData("elemId", ev.target.id);
        ev.originalEvent.dataTransfer.setData("eventId", this.model.cid);
    }
});

var EventsView = Backbone.View.extend({

    initialize: function(options) {
        this.project_pk = options.project_pk;
        this.tagId = this.project_pk == null ? "unallocated" : this.project_pk;
        this.$el = $("ul#events-" + this.tagId + ".event-list");
        this.render();
    },

    render: function() {
        this.collection = app.all_events.byProject(this.project_pk);
        this.$el.empty();
        _.each(this.collection.models, function(item) {
            this.renderEvent(item);
        }, this);
    },

    renderEvent: function(item) {
        var eventView = new EventView({
            model: item
        });
        this.$el.append(eventView.render().el);
    }
});

var ProjectView = Backbone.View.extend({
    template: app.templates.project_template,
    events: {
        'drop': 'addEvent'
    },
    render: function() {
        this.$el.html(this.template(this.model.attributes));
        return this;
    },
    addEvent: function(ev) {
        ev.preventDefault();
        var elemId = ev.originalEvent.dataTransfer.getData("elemId");
        var eventId = ev.originalEvent.dataTransfer.getData("eventId");
        var eventModel = app.all_events.get(eventId);
        eventModel.get("fields").project = this.model.get('pk');
        _.each(app.events_views, function(view) {view.render();})
    }
});

var UnallocatedContainerView = Backbone.View.extend({
    el: "#unallocated-container",
    events: {
        'drop': 'addEvent'
    },
    addEvent: function(ev) {
        ev.preventDefault();
        var elemId = ev.originalEvent.dataTransfer.getData("elemId");
        var eventId = ev.originalEvent.dataTransfer.getData("eventId");
        var eventModel = app.all_events.get(eventId);
        eventModel.get("fields").project = null;
        _.each(app.events_views, function(view) {view.render();})
    }
});

var ProjectsView = Backbone.View.extend({
    el: $('#project-list'),
    initialize: function() {
        this.collection.bind('add', this.renderProject, this);
    },
    render: function() {
        _.each(this.collection.models, function(item) {
            this.renderProject(item);
        }, this);
    },
    renderProject: function(item) {
        var projectView = new ProjectView({
            model: item
        });
        this.$el.append(projectView.render().el);
    },
});

var NewProjectModal = Backbone.View.extend({
    id: 'new-project-modal',
    className: 'modal fade',
    template: app.templates.new_project,
    events: {
        'hidden': 'teardown',
    },
    initialize: function() {
        _.bindAll(this, 'show', 'teardown', 'render', 'createProject');
        this.render();
        this.$el.find('#create').click(this.createProject);
    },
    show: function() {
        this.$el.modal('show');
    },
    teardown: function() {
        this.$el.data('modal', null);
        this.remove();
    },
    render: function() {
        this.$el.html(this.template({}));
        this.$el.modal({show:false});
        return this;
    },
    createProject: function() {
        var project = {};
        project.fields = {};
        project.fields.client_name = this.$el.find('#new-project-client').val();
        project.fields.project_name = this.$el.find('#new-project-name').val();
        var projectModel = new Project(project);
        projectModel.save(null, {success: function() {location.reload();}});
    }
});

////////////////////////////// UTILS

app.allowDrop = function allowDrop(ev) {
    ev.preventDefault();
}

// Construct and render projects views.
app.projects_collection = new Projects(app.data.projects);
app.projects_view = new ProjectsView({collection: app.projects_collection});
app.projects_view.render();

// Unallocated container
app.unallocated_container = new UnallocatedContainerView();

// All events
app.all_events = new Events(app.data.events);

// Construct and render events views.
app.events_views = {}
_.each(app.projects_collection.models, function(project) {
    var events_view = new EventsView({
        project_pk: project.get('pk'),
    });
    app.events_views[project.get('pk')] = events_view;
});

var events_view = new EventsView({
    project_pk: null
});

events_view.render();
app.events_views["unallocated"] = events_view;

$('#add-new-project').click(function() {
    var modalView = new NewProjectModal({collection: app.projects_collection});
    modalView.show();
});

$('#savebutton').click(function() {
    _.each(app.all_events.models, function(ev) {
        ev.save();
    });
});


///// CONFIGURE AJAX
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
    }
});

this.app = app;
});
