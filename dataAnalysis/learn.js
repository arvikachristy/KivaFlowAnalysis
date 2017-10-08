function learn(data) {
  const numberOfImportantLenders = data.reduce((sum, next) => sum + next.is_important_lender, 0);
  return numberOfImportantLenders
}

module.exports = learn;
