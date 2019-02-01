define(['base/js/utils', 'base/js/dialog'], function(utils, dialog) {
  'use strict';

  var base_url = utils.get_body_data('baseUrl');

  function open_external_ipynb(nb_url) {
    var url = utils.url_path_join(base_url, 'openurl') + "?url=" + nb_url;
    window.open(url);
  }

  function show_modal() {
    dialog.modal({
      title: "Open a Notebook from a URL",
      body: $('<div/>')
        .html('Enter the URL of a notebook you\'d like to open')
        .append($('<div/>').
          append($('<input/>')
            .attr('type', 'text')
            .attr('placeholder', 'url of .ipynb')
            .attr('size', 60)
            .attr('id', 'url_field'))),
      buttons: {
        Open: {
          class: 'btn-primary',
          click: function() { open_external_ipynb($('#url_field').val()); }
        }
      }
    });
  }

  return {
    load_ipython_extension: function() {
      $('<button/>')
      .attr('type', 'button')
      .attr('title', 'Load External Notebook')
      .attr('aria-label', 'load an external ipynb from a url')
      .addClass('btn btn-default btn-xs')
      .text('External')
      .on('click', function(e) { show_modal(); })
      .insertAfter('#new-buttons');
    }
  }
});
