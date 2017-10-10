// @flow
import type { State } from './utils/flow.types'

export const INITIAL_STATE = window.__INITIAL_STATE__ || {}

const state: State = {
  message: INITIAL_STATE.message,
  chromosome: 'chr1'
}

export default state
