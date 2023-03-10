interface BM25Props {
  code: string;
  score: number;
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
    hits: BM25Props[];
  };
}

export enum TyphonModel {
  // eslint-disable-next-line @typescript-eslint/naming-convention
  BM25 = "BM25",
  // eslint-disable-next-line @typescript-eslint/naming-convention
  MachineLearning = "Machine Learning",
}
