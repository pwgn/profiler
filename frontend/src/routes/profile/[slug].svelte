<script>
    import { onMount } from 'svelte'
    import { useParams } from '$app/params'

    let profileData = null

    // Retrieve profile data from server
    async function fetchProfileData() {
      const { profile_id } = $routeParams
      const response = await fetch(`http://localhost:8000/api/profile/${profile_id}`)
      if (response.ok) {
        profileData = await response.json()
      }
    }

    onMount(fetchProfileData)
  </script>

  {#if profileData}
    <h1>Profile {profileData.profile_id}</h1>
    <p>status: {profileData.status}</p>
    <p>path: {profileData.profile_path}</p>
  {/if}