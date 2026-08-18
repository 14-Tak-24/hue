import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export interface Soul {
  id: string;
  name: string;
  archetype: string;
  persona?: {
    description: string;
  };
  shadow?: {
    description: string;
  };
  platforms?: string[];
  rarity?: 'Legendary' | 'Rare' | 'Common';
  tier?: 'upper' | 'second';
  bio?: string;
  hooks?: string[];
  desires?: string[];
  kinks?: string[];
}

export const soulsApi = {
  // Get all souls
  getAllSouls: async (): Promise<Soul[]> => {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/souls`);
      return response.data;
    } catch (error) {
      console.error('Error fetching souls:', error);
      throw error;
    }
  },

  // Get soul by ID
  getSoulById: async (id: string): Promise<Soul> => {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/souls/${id}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching soul:', error);
      throw error;
    }
  },

  // Create soul
  createSoul: async (soul: Partial<Soul>): Promise<Soul> => {
    try {
      const response = await axios.post(`${API_BASE_URL}/api/souls`, soul);
      return response.data;
    } catch (error) {
      console.error('Error creating soul:', error);
      throw error;
    }
  },

  // Update soul
  updateSoul: async (id: string, soul: Partial<Soul>): Promise<Soul> => {
    try {
      const response = await axios.put(`${API_BASE_URL}/api/souls/${id}`, soul);
      return response.data;
    } catch (error) {
      console.error('Error updating soul:', error);
      throw error;
    }
  },

  // Delete soul
  deleteSoul: async (id: string): Promise<void> => {
    try {
      await axios.delete(`${API_BASE_URL}/api/souls/${id}`);
    } catch (error) {
      console.error('Error deleting soul:', error);
      throw error;
    }
  },

  // Get statistics
  getStatistics: async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/statistics`);
      return response.data;
    } catch (error) {
      console.error('Error fetching statistics:', error);
      throw error;
    }
  },
};