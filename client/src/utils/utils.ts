export const saveCurrentUrl = (currentUrl: string) => {
  localStorage.setItem('previousUrl', currentUrl);
}

export const getImageUrlFromCID = async (cid: string) => {
  try {
    let returnUrl;
    const response = await fetch(`https://api.nft.storage/${cid}`, {
      headers: { Authorization: "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkaWQ6ZXRocjoweDFGQzkwNjBCYkY1NjAzNEIxNzgyNTk0NTkzNUY4MDQyMzMxNWRBOTEiLCJpc3MiOiJuZnQtc3RvcmFnZSIsImlhdCI6MTcxMTE5NDM5MzIwMSwibmFtZSI6ImRlYWxlciJ9.90hFugZOVbYjIfml5hLOBzdkNZ2scvKMqllWlH1Uqzg" },
    });
    const data = await response.json();
    const imageName = data.value?.files[0]?.name;

    if (!imageName) {
      returnUrl = `https://${cid}.ipfs.nftstorage.link/`;
    } else {
      returnUrl = `https://ipfs.io/ipfs/${cid}/${imageName}`;
    }
    return returnUrl;
  } catch (error) {
    console.error('Error fetching image from CID:', error);
    return '';
  }
};

export async function updateClientWithImageUrls(client) {
  const imageUrls = await Promise.all(client.image_hashes.map((hash) => getImageUrlFromCID(hash)));

  return {
    ...client,
    imageUrls: imageUrls,
  };
}