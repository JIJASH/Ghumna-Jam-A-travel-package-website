
document.addEventListener('DOMContentLoaded', function() {
    const profileForm = document.getElementById('profile-form');
    const profilePictureFrame = document.querySelector('.profile-picture-frame img');

    profileForm.addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent the default form submission

        const formData = new FormData(profileForm);

        fetch(profileForm.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
            },
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Update the profile picture frame
                profilePictureFrame.src = data.profile_picture_url;
            }
        });
    });
});
