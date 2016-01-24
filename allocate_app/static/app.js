$(function($) {
var app = {};
app.EVENT_DATA_ID = 'events_json'
//////////////////////////// DATA
app.data = {};
app.data.events = JSON.parse($('#events_json').text());
app.data.events = _.pluck(app.data.events, 'fields');

app.data.projects = JSON.parse($('#projects_json').text());
app.data.projects = _.pluck(app.data.projects, 'fields');

var dummy_data = {
    'events': [
        {'id': Math.floor(Math.random() * 1000 % 1000), 'application': 'Calendar', 'description': 'Email to jony@apple.com',
         'start': new Date(2016, 1, 11, 9, 4, 20), 'end': new Date(2016, 1, 11, 9, 50, 55), 'project_id': null},
        {'id': Math.floor(Math.random() * 1000 % 1000), 'application': 'Calendar', 'description': 'APPL_INC_MARKETING_V1',
         'start': new Date(2016, 1, 11, 10, 15, 20), 'end': new Date(2016, 1, 11, 11, 25, 55), 'project_id': null},
        {'id': Math.floor(Math.random() * 1000 % 1000), 'application': 'Calendar', 'description': 'CocaCola_Prospective_Partners',
         'start': new Date(2016, 1, 11, 13, 40, 43), 'end': new Date(2016, 1, 11, 15, 04, 01), 'project_id': 1},
    ],
    'projects': [
        {'id': 1, 'client': 'Apple Inc.', 'project_name': 'Marketing Project'},
        {'id': 2, 'client': 'Coca Cola Co.', 'project_name': 'Sales sourcing'},
    ]
};

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
<li id="event-<%= event_id %>" class="draggable-event list-group-item" draggable="true" ondragstart="app.drag(event)">
    <%= application %>: <%= summary %><br>
    <%= _.template.formatdate(start) %> - <%= _.template.formatdate(end) %>
</li>
`);

app.templates.project_template = _.template(`
<div class="panel panel-default project" id="project-<%= id %>">
    <div class="panel-heading"><%= client %> - <%= project_name %></div>
    <div class="panel-body" ondrop="app.drop(event)" ondragover="app.allowDrop(event)">
        <ul id="events-<%= id %>" class="list-group event-list">
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
            <label for="new-project-pattern">Project pattern</label>
            <input type="text" class="form-control" id="new-project-pattern" placeholder="iPhone [L|l]aunch">
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
    defaults: {
        application: 'Calendar',
        name: 'No description available',
    }
});

var Events = Backbone.Collection.extend({
    model: Event,
    byProject: function(project_id) {
        filtered = this.filter(function(ev) {
            return ev.get('project_id') == project_id;
        });
        return new Events(filtered);
    }
});

var Project = Backbone.Model.extend({
    defaults: {
        id: 1,
        client: 'NA',
        project_name: 'NA'
    }
});

var Projects = Backbone.Collection.extend({
    model: Project
});

/////////////////////////////////////// VIEWS

var EventView = Backbone.View.extend({
    template: app.templates.event_template,
    render: function() {
        this.$el.html(this.template(this.model.attributes));
        return this;
    },
});

var EventsView = Backbone.View.extend({

    initialize: function(options) {
        this.collection = options.collection;
        this.$el = $("ul#events-" + options.tagId + ".event-list");
    },

    render: function() {
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
    render: function() {
        this.$el.html(this.template(this.model.attributes));
        return this;
    },
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
        var maxId = -1;
        _.each(this.collection.models, function(proj) {
            if (proj.id > maxId) {
                maxId = proj.id;
            }
        }, this);
        project.id = maxId + 1;
        project.client = this.$el.find('#new-project-client').val();
        project.project_name = this.$el.find('#new-project-name').val();
        var projectModel = new Project(project);
        this.collection.add(projectModel);
        this.$el.modal('hide');
    }
});

////////////////////////////// UTILS

app.allowDrop = function allowDrop(ev) {
    ev.preventDefault();
}

app.drag = function drag(ev) {
    ev.dataTransfer.setData("text", ev.target.id);
}

app.drop = function drop(ev) {
    ev.preventDefault();
    var data = ev.dataTransfer.getData("text");
    var target_ul = $(ev.target).children("ul");
    target_ul.append(document.getElementById(data));
}


// Construct and render projects views.
app.projects_collection = new Projects(app.data.projects);
app.projects_view = new ProjectsView({collection: app.projects_collection});
app.projects_view.render();

// All events
app.all_events = new Events(app.data.events);

// Construct and render events views.
app.events_views = {}
_.each(app.data.projects, function(project) {
    var collection = app.all_events.byProject(project.id);
    var events_view = new EventsView({
        tagId: project.id,
        collection: collection
    });
    events_view.render();
    app.events_views[project.id] = events_view;
});

var collection = app.all_events.byProject(null);
var events_view = new EventsView({
    tagId: "unallocated",
    collection: collection
});

events_view.render();
app.events_views["unallocated"] = events_view;

$('#add-new-project').click(function() {
    var modalView = new NewProjectModal({collection: app.projects_collection});
    modalView.show();
})

this.app = app;
});
