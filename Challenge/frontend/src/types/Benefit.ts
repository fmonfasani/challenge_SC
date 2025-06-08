export interface Benefit {
  id: number;
  name: string;
  description: string;
  image: string;
  status: 'active' | 'inactive';
  fullDescription?: string;
  category?: string;
  validUntil?: string;
}
