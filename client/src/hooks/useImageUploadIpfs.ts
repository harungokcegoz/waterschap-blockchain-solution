import { writable } from 'svelte/store';

export function useImageUploadIpfs() {
  const isLoading = writable(false);

  const uploadImage = async (file: string | Blob) => {
    if (!file) {
      console.log('No file provided');
      return null;
    }

    isLoading.set(true);

    const uploadData = new FormData();
    uploadData.append('file', file);

    try {
      const response = await fetch('https://api.nft.storage/upload', {
        method: 'POST',
        headers: { Authorization: "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkaWQ6ZXRocjoweDFGQzkwNjBCYkY1NjAzNEIxNzgyNTk0NTkzNUY4MDQyMzMxNWRBOTEiLCJpc3MiOiJuZnQtc3RvcmFnZSIsImlhdCI6MTcxMTE5NDM5MzIwMSwibmFtZSI6ImRlYWxlciJ9.90hFugZOVbYjIfml5hLOBzdkNZ2scvKMqllWlH1Uqzg" },
        body: uploadData,
      });

      if (!response.ok) {
        throw new Error('Failed to upload image');
      }

      const data = await response.json();
      
      return data.value.cid;
    } catch (err) {
      console.error(err);
      return null;
    } finally {
      isLoading.set(false);
    }
  };

  return {
    isLoading,
    uploadImage,
  };
}
