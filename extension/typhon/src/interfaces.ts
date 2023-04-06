interface HitProps {
  code: string;
  score: number;
  id?: string;
}

export interface IPreProcessResponse {
  // eslint-disable-next-line @typescript-eslint/naming-convention
  original_markdowns: string[];
  // eslint-disable-next-line @typescript-eslint/naming-convention
  preprocessed_markdown: string[];
}

export interface IResponse {
  error?: string;
  data?: {
    totalHits: number;
    hits: HitProps[];
  };
}

export enum TyphonModel {
  // eslint-disable-next-line @typescript-eslint/naming-convention
  BM25 = "BM25",
  // eslint-disable-next-line @typescript-eslint/naming-convention
  MachineLearning = "Machine Learning",
}

export enum TyphonDataTier {
  GRANDMASTER = "Grandmaster",
  MASTER = "Master",
  EXPERT = "Expert",
}