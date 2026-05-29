import { existsSync, readFileSync } from "fs";
import path from "path";
import type { ProofLibrary } from "./proof-library-types";

export type { ProofLibrary, ProofLibraryEntry, ProofVoteOption } from "./proof-library-types";
export {
  VOTE_LABELS,
  PROOF_LIBRARY_PUBLIC_URL,
  proofStatusBadgeClass,
} from "./proof-library-types";

const LIB_PATH = path.join(process.cwd(), "..", "data", "latest", "proof-library.json");

export function loadProofLibrary(): ProofLibrary | null {
  if (!existsSync(LIB_PATH)) return null;
  const raw = readFileSync(LIB_PATH, "utf8");
  return JSON.parse(raw) as ProofLibrary;
}
