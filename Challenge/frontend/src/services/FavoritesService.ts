export const FavoritesService = {
  getFavorites: (): number[] => {
    const favorites = localStorage.getItem('favorites');
    return favorites ? JSON.parse(favorites) : [];
  },

  addFavorite: (id: number): void => {
    const favorites = FavoritesService.getFavorites();
    if (!favorites.includes(id)) {
      favorites.push(id);
      localStorage.setItem('favorites', JSON.stringify(favorites));
    }
  },

  removeFavorite: (id: number): void => {
    const favorites = FavoritesService.getFavorites();
    const filtered = favorites.filter(fav => fav !== id);
    localStorage.setItem('favorites', JSON.stringify(filtered));
  },

  isFavorite: (id: number): boolean => {
    return FavoritesService.getFavorites().includes(id);
  }
};
