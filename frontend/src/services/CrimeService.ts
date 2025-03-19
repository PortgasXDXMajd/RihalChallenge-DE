import { axios } from '@/utils/helpers/AxiosHelper';

class CrimeService {
  static async get_state(): Promise<CrimeData[] | null> {
    const response = await axios.get('/crime/required-stats');
    if (response.status === 200) {
      return response.data.body;
    }
    return null;
  }
}

export default CrimeService;
