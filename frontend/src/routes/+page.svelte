<script>
    import { onMount } from "svelte";
    import { goto } from "$app/navigation";
    import axios from "axios";

    let files = [];

    const handleFileInput = (event) => {
        files = [...event.target.files];
    };

    const handleSubmit = async () => {
        const formData = new FormData();
        formData.append("files", files[0]);

        try {
            const response = await axios.post(
                "http://localhost:8000/api/profile",
                formData
            );
            let profile_id = response.data.profile_id;
            console.log("Profile ID:", profile_id);
            goto(`profile/${profile_id}`);
        } catch (error) {
            console.error("Error uploading file:", error);
        }
    };
</script>

<div>
    <input type="file" on:change={handleFileInput} />
    <button on:click={handleSubmit}>Upload File</button>
</div>
