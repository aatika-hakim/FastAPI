$(document).ready(function() {
    // Load notes when the page loads
    loadNotes();

    // Handle form submission to create a new note
    $('#createNoteForm').submit(function(event) {
        event.preventDefault();
        
        var title = $('#title').val();
        var content = $('#content').val();

        $.ajax({
            type: 'POST',
            url: 'http://localhost:8000/notes/',
            contentType: 'application/json',
            data: JSON.stringify({
                title: title,
                content: content
            }),
            success: function(response) {
                $('#title').val('');
                $('#content').val('');
                loadNotes();
            },
            error: function(error) {
                console.log('Error creating note:', error);
            }
        });
    });

    // Function to load all notes
    function loadNotes() {
        $.ajax({
            type: 'GET',
            url: 'http://localhost:8000/notes/',
            success: function(notes) {
                var notesContainer = $('#notesContainer');
                notesContainer.empty();
                notes.forEach(function(note) {
                    var noteElement = $('<div class="note">')
                        .append('<h3 class="edited-title">' + note.title + '</h3>')
                        .append('<p class="edited-title">' + note.content + '</p>')
                        .append('<button class="edit-btn" data-id="' + note.id + '">Edit</button>')
                        .append('<button class="save-btn" data-id="' + note.id + '" style="display:none;">Save</button>')
                        .append('<button class="delete-btn" data-id="' + note.id + '">Delete</button>');

                    notesContainer.append(noteElement);
                });

                // Bind edit and delete events after rendering notes
                bindNoteEvents();
            },
            error: function(error) {
                console.log('Error loading notes:', error);
            }
        });
    }

    // Function to bind edit and delete events to note buttons
    function bindNoteEvents() {
        $('.edit-btn').click(function() {
            var $note = $(this).closest('.note');
            var noteId = $(this).data('id');
            var $content = $note.find('p');
            var currentContent = $content.text();

            // Replace paragraph with textarea for editing
            $content.replaceWith('<textarea class="edit-content">' + currentContent + '</textarea>');

            // Toggle buttons display
            $(this).hide();
            $note.find('.save-btn').show();
        });

        $('.save-btn').click(function() {
            var noteId = $(this).data('id');
            var updatedContent = $(this).siblings('.edit-content').val();

            $.ajax({
                type: 'PUT',
                url: 'http://localhost:8000/notes/' + noteId,
                contentType: 'application/json',
                data: JSON.stringify({
                    title: 'Updated', 
                    content: updatedContent
                }),
                success: function(response) {
                    loadNotes(); // Reload notes after successful update
                },
                error: function(error) {
                    console.log('Error updating note:', error);
                }
            });
        });

        $('.delete-btn').click(function() {
            var noteId = $(this).data('id');
            $.ajax({
                type: 'DELETE',
                url: 'http://localhost:8000/notes/' + noteId,
                success: function(response) {
                    loadNotes(); // Reload notes after successful delete
                },
                error: function(error) {
                    console.log('Error deleting note:', error);
                }
            });
        });
    }
});
